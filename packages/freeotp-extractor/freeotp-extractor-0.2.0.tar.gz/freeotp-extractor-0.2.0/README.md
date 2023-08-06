# FreeOTP tokens extractor

## Backing up FreeOTP

Using [adb](https://developer.android.com/studio/command-line/adb.html), [create a backup](https://androidquest.wordpress.com/2014/09/18/backup-applications-on-android-phone-with-adb/) of the app using the following command:

```sh
adb backup -f freeotp-backup.ab -apk org.fedorahosted.freeotp
```

[org.fedorahosted.freeotp](https://play.google.com/store/apps/details?id=org.fedorahosted.freeotp) is the app ID for FreeOTP.

This will ask, on the phone, for a password to encrypt the backup. Proceed with a password.

## Manually extracting the backup

The backups are some form of encrypted tar file. [Android Backup Extractor](https://github.com/nelenkov/android-backup-extractor) can decrypt them.

It's available on the AUR as [android-backup-extractor-git](https://aur.archlinux.org/packages/android-backup-extractor-git/).

Use it like so (this command will ask you for the password you just set to decrypt it):

```sh
abe unpack freeotp-backup.ab freeotp-backup.tar
```

Then extract the generated tar file:

```shell
$ tar xvf freeotp-backup.tar
apps/org.fedorahosted.freeotp/_manifest
apps/org.fedorahosted.freeotp/sp/tokens.xml
```

We don't care about the manifest file, so let's look at `apps/org.fedorahosted.freeotp/sp/tokens.xml`.

## Extract tokens

First, download [`freeotp_extractor.py`](https://gitlab.com/Oprax/freeotp-extractor/blob/master/freeotp_extractor.py), then you can run `python freeotp_extractor.py -h` :

```
usage: freeotp_extractor.py [-h] [-v] [-o OUTPUT] input

Extract token from FreeOTP

positional arguments:
  input                 File containing XML with tokens (usually 'tokens.xml')

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        Give the output file for save tokens
```

To just have tokens, run `python freeotp_extractor.py apps/org.fedorahosted.freeotp/sp/tokens.xml`
It will output something like :
```
Dropbox:example@gmail.com: BQ4F6XX3QOFEXQY5SNFPJZW3
gitlab.com:example@gmail.com: 4FBTY2GE3VK7BMFBFOE3X7CR
Google:example@gmail.com: RK6MVRZCQXFBUMGBKZBF5CAA
```
Or you can pass a `output` parameter to save it into a file `python freeotp_extractor.py -o tokens.json apps/org.fedorahosted.freeotp/sp/tokens.xml`

`tokens.json`:
```json
{
  "Dropbox:example@gmail.com":"BQ4F6XX3QOFEXQY5SNFPJZW3",
  "gitlab.com:example@gmail.com":"4FBTY2GE3VK7BMFBFOE3X7CR",
  "Google:example@gmail.com":"RK6MVRZCQXFBUMGBKZBF5CAA"
}
```
