import secrets
import hashlib


def sha256(data):
    if isinstance(data, str):
        data = data.encode("utf-8")

    return hashlib.sha256(data).digest()


def random_generator():
    words = []
    chars = 'abcdefghijklmnopqrstuvwxyz'
    with open('random.txt') as wordlist:
        for line in wordlist.readlines():
            parts = line.split('\t')
            if len(parts) > 1:
                words.append(parts[1].strip())

    def generate():
        phrase = [secrets.choice(words) for _ in range(6)]
        phrase.insert(secrets.randbelow(6), ''.join([secrets.choice(chars) for _ in range(8)]))
        return ' '.join(phrase)

    return generate()


def getbinarystring(digest):
    bits = ""
    for byte in digest:
        bits += bin(byte)[2:].rjust(8, "0")
    return bits


def getmnemonicphrase(password):
    # sha256 of the text
    digest = sha256(password)

    # calculate the hash bits
    hashbits = getbinarystring(sha256(digest))[:8]

    # string of bits from the digest
    binarystring = getbinarystring(digest) + hashbits

    # wordlist of mnemonics
    wordlist = open("lib.txt", "r").read().split("\n")

    # bits spllited in groups of 11 bits
    entropygroups = [binarystring[i:i + 11] for i in range(0, len(binarystring), 11)]

    # convert these groups of bits into integers that will be used as indexes
    mnemonicindexes = map(lambda x: int(x, 2), entropygroups)

    # map mnemonics
    mnemonics = list(map(lambda x: wordlist[x], mnemonicindexes))
    return " ".join(mnemonics)


def main():
    text = input("Enter your password phrase:\n")
    if text == "":
        text = random_generator()
    result = getmnemonicphrase(text)
    print("Your mnemonic phrase is:")
    print(result)


if __name__ == "__main__":
    main()
