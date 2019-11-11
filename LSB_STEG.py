from PIL import Image
import sys, os
import binascii


def encode(ori_img, secret):
	BINsecret = "".join(format(ord(i),"08b") for i in secret)
	IMG = Image.open(ori_img).convert("RGBA")
	W, H = IMG.size
	for i in xrange(H):
		for j in xrange(W):
			R, G, B, Alpha = IMG.getpixel((i, j))
			if BINsecret[(3*(i*W + j + 1) - 3) % len(BINsecret)] == "0":
				Red = R & 0xfe ^ 0x0
			else:
				Red = R & 0xfe ^ 0x1

			if BINsecret[(3*(i*W + j + 1) - 2) % len(BINsecret)] == "0":
				Green = G & 0xfe ^ 0x0
			else:
				Green = G & 0xfe ^ 0x1

			if BINsecret[(3*(i*W + j + 1) - 1) % len(BINsecret)] == "0":
				Blue = B & 0xfe ^ 0x0
			else:
				Blue = B & 0xfe ^ 0x1
			IMG.putpixel((i, j), (Red, Green, Blue, Alpha))
	steg_img = IMG.save("LSB_Steg.png")
	IMG.show()
	print("==> DONE")


def decode(steg_img):
	BINsecret = ""
	IMG = Image.open(steg_img).convert("RGBA")
	W, H = IMG.size
	for i in xrange(W):
		for j in xrange(H):
			R, G, B, A = IMG.getpixel((i, j))
			Red = str(R & 0x1)
			Green = str(G & 0x1)
			Blue = str(B & 0x1)
			BINsecret += Red + Green + Blue
	print("Your text: " + binascii.unhexlify("%x" % int(BINsecret, 2)))


def main():
	if len(sys.argv) == 2:
		steg_img = sys.argv[1]
		if os.path.isfile(steg_img):
			decode(steg_img)
	elif len(sys.argv) == 3:
		ori_img = sys.argv[1]
		secret = sys.argv[2]
		if os.path.isfile(ori_img):
			encode(ori_img, secret)
	exit("RUN: python {} steg_img | ori_img secret".format(sys.argv[0]))


if __name__ == "__main__":
	main()