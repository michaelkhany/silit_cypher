from PIL import Image
import numpy as np
import argparse
import os

def encode_message_into_image(image_path, message, output_path=None):
    # Load the image
    image = Image.open(image_path)
    
    # Convert the image to PNG format to avoid lossy compression issues
    temp_path = "temp_image.png"
    image.save(temp_path)
    image = Image.open(temp_path)
    pixels = np.array(image)
    
    # Prepare the message
    binary_message = ''.join(format(ord(c), '07b') for c in message) + '0000000'  # Using '0000000' as the end marker
    message_index = 0
    
    # Encode the message into the image
    for index, value in np.ndenumerate(pixels):
        if message_index < len(binary_message):
            bit = binary_message[message_index]
            if bit == '1':
                pixels[index] |= 1  # Set LSB to 1
            else:
                pixels[index] &= ~1  # Set LSB to 0
            message_index += 1
        else:
            break  # Stop when the message is fully encoded
    
    # Save the modified image
    encoded_image = Image.fromarray(pixels)
    if output_path is None:
        output_file_name = f"encoded_{os.path.basename(image_path)}"
        output_path = os.path.splitext(output_file_name)[0] + ".png"  # Ensure the output is a PNG file
    encoded_image.save(output_path)
    
    # Clean up the temporary PNG conversion if it's different from the output path
    if temp_path != output_path:
        os.remove(temp_path)
    
    print(f"Message encoded into image and saved as {output_path}")

def decode_message_from_image(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    
    binary_message = ''
    for value in np.nditer(pixels):
        binary_message += str(value & 1)  # Extract LSB
    
    # Split the binary message into 7-bit chunks and convert to characters
    chars = [binary_message[i:i+7] for i in range(0, len(binary_message), 7)]
    message = ''.join([chr(int(c, 2)) for c in chars if int(c, 2) != 0])
    
    print("Decoded message:", message)

## To run the script using system
# def main():
    # parser = argparse.ArgumentParser(description='Steganography tool for encoding and decoding messages in images.')
    # parser.add_argument('operation', choices=['encode', 'decode'], help='Operation to perform: encode or decode.')
    # parser.add_argument('image_path', type=str, help='Path to the target image.')
    # parser.add_argument('--message', type=str, default='', help='Message to encode (required for encode operation).')
    # parser.add_argument('--output', type=str, default=None, help='Output path for the encoded image (optional).')
    
    # args = parser.parse_args()
    
    # if args.operation == 'encode':
    #     if not args.message:
    #         raise ValueError("Message is required for encoding.")
    #     encode_message_into_image(args.image_path, args.message, args.output)
    # elif args.operation == 'decode':
    #     decode_message_from_image(args.image_path)

## To run it directly
def main():
    print("Steganography Tool")
    print("1. Encode a message into an image")
    print("2. Decode a message from an image")
    choice = input("Choose an operation (1 or 2): ")

    if choice == '1':
        image_path = input("Enter the path to the image for encoding: ")
        message = input("Enter the message to encode: ")
        output_path = input("Enter the output image path (optional, press Enter to skip): ")
        if not output_path:
            output_path = None
        encode_message_into_image(image_path, message, output_path)
    elif choice == '2':
        image_path = input("Enter the path to the encoded image: ")
        decode_message_from_image(image_path)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == '__main__':
    main()

    main()
