#!/usr/bin/env python3
import pickle
import sys
import os
import struct
import getpass
from hashlib import sha256
from random import randint
import argparse
import subprocess

try:
    import py_sg
except ImportError:
    print("You need to install the 'py_sg' module.")
    sys.exit(1)

BLOCK_SIZE = 512
HANDSTORESECURITYBLOCK = 1
dev = None

def parse_args(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "-s",
        "--status",
        required=False,
        action="store_true",
        help="Check device status and encryption type")

    parser.add_argument(
        "-u",
        "--unlock",
        required=False,
        action="store_true",
        help="Unlock")

    parser.add_argument(
        "-us",
        "--unlock-with-saved-passwd",
        required=False,
        action="store_true",
        help="Unlock with saved passwd")

    parser.add_argument(
        "-m",
        "--mount",
        required=False,
        action="store_true",
        help="Enable mount point for an unlocked device")

    parser.add_argument(
        "-c",
        "--change-passwd",
        required=False,
        action="store_true",
        help="Change (or disable) password")

    parser.add_argument(
        "-sp",
        "--save-passwd",
        required=False,
        action="store_true",
        help="Save passwd")

    parser.add_argument(
        "-e",
        "--erase",
        required=False,
        action="store_true",
        help="Secure erase device")

    parser.add_argument(
        "-d",
        "--device",
        dest="device",
        required=False,
        help="Force device path (ex. /dev/sdb). Usually you don't need this option.")

    return parser.parse_args(argv)

def fail(msg):
    '''Print fail message with red leading characters'''
    print("\033[91m" + "[!]" + "\033[0m" + " " + msg)


def success(msg):
    '''Print fail message with green leading characters'''
    print("\033[92m" + "[*]" + "\033[0m" + " " + msg)


def question(msg):
    '''Print fail message with blue leading characters'''
    print("\033[94m" + "[+]" + "\033[0m" + " " + msg)


def title(msg):
    print("\033[93m" + msg + "\033[0m")


def check_root_user():
    '''Exit if the current user has not root privileges'''
    if os.geteuid() != 0:
        fail("You need to have root privileges to run this script.")
        sys.exit(1)


def sec_status_to_str(security_status):
    '''Convert an integer to his human-readable secure status'''
    status = {
        0x00: "No lock",
        0x01: "Locked",
        0x02: "Unlocked",
        0x06: "Locked, unlock blocked",
        0x07: "No keys"
    }
    if security_status in status.keys():
        return status[security_status]
    else:
        return "unknown"


def cipher_id_to_str(id):
    '''Convert an integer to his human-readable cipher algorithm'''
    ciphers = {
        0x10: "AES_128_ECB",
        0x12: "AES_128_CBC",
        0x18: "AES_128_XTS",
        0x20: "AES_256_ECB",
        0x22: "AES_256_CBC",
        0x28: "AES_256_XTS",
        0x30: "Full Disk Encryption"
    }
    if id in ciphers.keys():
        return ciphers[id]
    else:
        return "unknown"


def _scsi_pack_cdb(cdb):
    '''Transform "cdb" in char[]'''
    return struct.pack('{0}B'.format(len(cdb)), *cdb)


def htonl(num):
    '''Convert int from host byte order to network byte order'''
    return struct.pack('!I', num)


def htons(num):
    '''Convert int from  host byte order to network byte order'''
    return struct.pack('!H', num)


def read_handy_store(page):
    '''Call the device and get the selected block of Handy Store.'''
    cdb = [0xD8, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x01, 0x00]
    i = 2
    for c in htonl(page):
        cdb[i] = c
        i += 1
    return py_sg.read_as_bin_str(dev, _scsi_pack_cdb(cdb), BLOCK_SIZE)


def hsb_checksum(data):
    '''Calculate checksum on the returned data'''
    c = 0
    for i in range(510):
        c = c + data[i]
    c = c + data[0]  # Some WD Utils count data[0] twice, some other not ...
    r = (c * -1) & 0xFF
    return hex(r)


def get_encryption_status():
    '''
    Call the device and get the encryption status.
    The function returns three values:
        SecurityStatus: 
            0x00 => No lock
            0x01 => Locked
            0x02 => Unlocked
            0x06 => Locked, unlock blocked
            0x07 => No keys
        CurrentChiperID
            0x10 =>	AES_128_ECB
            0x12 =>	AES_128_CBC
            0x18 =>	AES_128_XTS
            0x20 =>	AES_256_ECB
            0x22 =>	AES_256_CBC
            0x28 =>	AES_256_XTS
            0x30 =>	Full Disk Encryption
        KeyResetEnabler (4 bytes that change every time)
    '''
    cdb = [0xC0, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x00]
    data = py_sg.read_as_bin_str(dev, _scsi_pack_cdb(cdb), BLOCK_SIZE)
    if data[0] != 0x45:
        fail(f"Wrong encryption status signature {data[0]:#x}")
        sys.exit(1)
    # (SecurityStatus, CurrentChiperID, KeyResetEnabler)
    return (data[3], data[4], data[8:12])


def read_HSB1():
    '''
    Call the device and get the first block of Handy Store.
    The function returns three values:
        Iteration - number of iteration (hashing) in password generation
        Salt - salt used in password generation
        Hint - hint of the password if used. TODO.
    '''
    signature = [0x00, 0x01, 0x44, 0x57]
    sector_data = read_handy_store(1)
    # Check if retrieved Checksum is correct
    if hsb_checksum(sector_data) != hex(sector_data[511]):
        fail("Wrong HSB1 checksum")
        sys.exit(1)
    # Check if retrieved Signature is correct
    for i in range(0, 4):
        if signature[i] != sector_data[i]:
            fail("Wrong HSB1 signature.")
            sys.exit(1)

    iteration = struct.unpack_from("<I", sector_data[8:])
    salt = sector_data[12:20] + bytes([0x00, 0x00])
    hint = sector_data[24:226] + bytes([0x00, 0x00])
    return (iteration[0], salt, hint)


def mk_password_block(passwd, iteration, salt):
    '''Perform password hashing with requirements obtained from the device'''
    clean_salt = ""
    for i in range(int(len(salt)/2)):
        if salt[2*i] == salt[2*i+1] == 0x00:
            break
        clean_salt = clean_salt + chr(salt[2*i])

    password = clean_salt + passwd
    password = password.encode("utf-16")[2:]

    for _ in range(iteration):
        password = sha256(password).digest()

    return password


def unlock(save_passwd, unlock_with_saved_passwd):
    '''Unlock the device'''
    cdb = [0xC1, 0xE1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x28, 0x00]
    sec_status, cipher_id, _ = get_encryption_status()

    # Device should be in the correct state
    if sec_status in [0x00, 0x02]:
        fail("Your device is already unlocked!")
        return
    elif sec_status != 0x01:
        fail("Wrong device status!")
        sys.exit(1)

    if cipher_id in [0x10, 0x12, 0x18]:
        pwblen = 16
    elif cipher_id in [0x20, 0x22, 0x28]:
        pwblen = 32
    elif cipher_id == 0x30:
        pwblen = 32
    else:
        fail(f"Unsupported cipher {cipher_id:#x}")
        sys.exit(1)

    # Get password from user
    if not unlock_with_saved_passwd:
        question("Insert password to Unlock the device:")
        passwd = getpass.getpass()
        iteration, salt, _ = read_HSB1()
        pwd_hashed = mk_password_block(passwd, iteration, salt)
    else:
        success("Unlock use saved password")
        passwd_bin = open("passwd.bin", "r")
        pwd_hashed = pickle.load(passwd_bin)

    if save_passwd:
        passwd_bin = open("passwd.bin", "w+b")
        pickle.dump(pwd_hashed, passwd_bin)

    pw_block = [0x45, 0x00, 0x00, 0x00, 0x00, 0x00]
    for c in htons(pwblen):
        pw_block.append(c)

    cdb[8] = pwblen + 8

    try:
        py_sg.write(dev, _scsi_pack_cdb(cdb), _scsi_pack_cdb(pw_block) + pwd_hashed)
        success("Device unlocked.")
    except:
        fail("Wrong password? Or something bad is happened. Try again")
        pass


def change_password():
    '''
    Change device password.
    If the new password is empty the device state changes and becomes "0x00 - No lock" meaning encryption is no more used.
    If the device is unencrypted a user can choose a password and make the whole device encrypted.

    DEVICE HAS TO BE UNLOCKED TO PERFORM THIS OPERATION.
    '''
    cdb = [0xC1, 0xE2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0x00]
    sec_status, cipher_id, _ = get_encryption_status()
    if sec_status not in [0x02, 0x00]:
        fail("Device has to be unlocked or without encryption to perform this operation")
        sys.exit(1)
    if cipher_id in [0x10, 0x12, 0x18]:
        pwblen = 16
    elif cipher_id in [0x20, 0x22, 0x28]:
        pwblen = 32
    elif cipher_id == 0x30:
        pwblen = 32
    else:
        fail(f"Unsupported cipher {cipher_id:#x}")
        sys.exit(1)

    question("Insert the OLD password")
    old_passwd = getpass.getpass()
    question("Insert the NEW password")
    new_passwd = getpass.getpass()
    question("Confirm the NEW password")
    new_passwd2 = getpass.getpass()
    if new_passwd != new_passwd2:
        fail("Password confirmation doesn't match the given password")
        sys.exit(1)

    if len(old_passwd) == len(new_passwd) == 0:
        fail("Both passwords shouldn't be empty")
        sys.exit(1)

    iteration, salt, _ = read_HSB1()
    pw_block = [0x45, 0x00, 0x00, 0x00, 0x00, 0x00]
    for c in htons(pwblen):
        pw_block.append(c)

    if (len(old_passwd) > 0):
        old_passwd_hashed = mk_password_block(old_passwd, iteration, salt)
        pw_block[3] = pw_block[3] | 0x10
    else:
        old_passwd_hashed = ""
        for _ in range(32):
            old_passwd_hashed = old_passwd_hashed + chr(0x00)

    if (len(new_passwd) > 0):
        new_passwd_hashed = mk_password_block(new_passwd, iteration, salt)
        pw_block[3] = pw_block[3] | 0x01
    else:
        new_passwd_hashed = ""
        for _ in range(32):
            new_passwd_hashed = new_passwd_hashed + chr(0x00)

    if pw_block[3] & 0x11 == 0x11:
        pw_block[3] = pw_block[3] & 0xEE

    cdb[8] = 8 + 2 * pwblen
    try:
        py_sg.write(dev, _scsi_pack_cdb(cdb), _scsi_pack_cdb(pw_block) + old_passwd_hashed + new_passwd_hashed)
        success("Password changed.")
    except:
        fail("Error changing password: Wrong password or something bad is happened.")
        pass
    

def secure_erase(cipher_id=0):
    '''
    Change the internal key used for encryption, every data on the device would be permanently unaccessible.
    Device forgets even the partition table so you have to make a new one.
    '''
    cdb = [0xC1, 0xE3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00]
    _, current_cipher_id, key_reset = get_encryption_status()

    if cipher_id == 0:
        cipher_id = current_cipher_id

    pw_block = [0x45, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00]

    if cipher_id in [0x10, 0x12, 0x18]:
        pwblen = 16
        pw_block[3] = 0x01
    elif cipher_id in [0x20, 0x22, 0x28]:
        pwblen = 32
        pw_block[3] = 0x01
    elif cipher_id == 0x30:
        pwblen = 32
        #pw_block[3] = 0x00
    else:
        fail(f"Unsupported cipher {cipher_id:#x}")
        sys.exit(1)

    # Set the actual lenght of pw_block (8 bytes + pwblen pseudorandom data)
    cdb[8] = pwblen + 8
    # Fill pw_block with random data
    for rand_byte in os.urandom(pwblen):
        pw_block.append(rand_byte)

    # key_reset needs to be retrieved immidiatly before the reset request
    key_reset = get_encryption_status()[2]
    i = 2
    for c in key_reset:
        cdb[i] = c
        i += 1

    try:
        py_sg.write(dev, _scsi_pack_cdb(cdb), _scsi_pack_cdb(pw_block))
        success(
            "Device erased. You need to create a new partition on the device (Hint: fdisk and mkfs)")
    except:
        fail("Something wrong.")
        pass


def get_device_info(device=None):
    '''
    Get device info through "lsscsi" command
    For example from the following string:
        "[23:0:0:0]   disk    WD       My Passport 0820 1012  /dev/sdb"
    these will be extracted:
        complete_path = '/dev/sdb'
        relative_path = 'sdb'
        host_number = '23'
    '''
    if device == None:
        grep_string = "Passport"
    else:
        grep_string = str(device, 'utf-8')

    dev_reg = r'"\/([a-zA-Z]+)\/([a-zA-Z0-9]+)"'
    complete_path = subprocess.Popen(
        f"lsscsi | grep {grep_string} | grep -oP {dev_reg}",
        shell=True,
        stdout=subprocess.PIPE
    ).stdout.read().rstrip()

    relative_path = subprocess.Popen(
        f"lsscsi | grep {grep_string} | grep -oP {dev_reg} | cut -d '/' -f 3",
        shell=True,
        stdout=subprocess.PIPE
    ).stdout.read().rstrip()

    host_number = subprocess.Popen(
        f"lsscsi -d | grep {grep_string} | cut -d ':' -f 1 | cut -d '[' -f 2",
        shell=True,
        stdout=subprocess.PIPE
    ).stdout.read().rstrip()

    return [complete_path, relative_path, host_number]


def enable_mount(device):
    '''
    Enable mount operations.
    Tells the system to scan the "new" (unlocked) device.
    '''
    sec_status = get_encryption_status()[0]
    # Device should be in the correct state
    if sec_status in [0x00, 0x02]:
        info = get_device_info(device)
        rp = str(info[1], 'utf-8')
        hn = str(info[2], 'utf-8')
        subprocess.Popen(
            f"echo 1 > /sys/block/{rp}/device/delete",
            shell=True
        )
        
        subprocess.Popen(
            f"echo \"- - -\" > /sys/class/scsi_host/host{hn}/scan",
            shell=True
        )

        success(
            "Now depending on your system you can mount your device or it will be automagically mounted.")
    else:
        fail("Device needs to be unlocked in order to mount it.")


def get_device(device):
    if device:
        return device
    else:
        # Get occurrences of "Passport" devices
        p = subprocess.Popen(
            "lsscsi | grep Passport | wc -l",
            shell=True,
            stdout=subprocess.PIPE)

        if int(p.stdout.read().rstrip()) > 1:
            fail("Multiple occurences of 'My Passport' detected.")
            fail("You should specify a device manually (with -d option).")
            sys.exit(1)

        return get_device_info()[0]

# Main function, get parameters and manage operations
def main():
    global dev
    title("WD Passport Ultra linux utility v0.1 by duke")
    args = parse_args(sys.argv[1:])
    if len(sys.argv) == 1:
        args.status = True
        
    check_root_user() 
    DEVICE = get_device(args.device)
    try:
        dev = open(DEVICE, "r+b")
    except:
        fail(f"Something wrong opening device '{str(DEVICE, 'utf-8')}'")
        sys.exit(1)

    if args.status:
        status, cipher_id, _ = get_encryption_status()
        success("Device state")
        print(f"\tSecurity status: {sec_status_to_str(status)}")
        print(f"\tEncryption type: {cipher_id_to_str(cipher_id)}")
    if args.unlock:
        unlock(args.save_passwd, False)

    if args.unlock_with_saved_passwd:
        unlock(args.save_passwd, True)

    if args.change_passwd:
        change_password()


    if args.erase:
        question(
            "Any data on the device will be lost. Are you sure you want to continue? [y/N]")
        r = sys.stdin.read(1)
        if r.lower() == 'y':
            secure_erase(0)
        else:
            success("Ok. Bye.")

    if args.mount:
        enable_mount(DEVICE)


if __name__ == "__main__":
    main()