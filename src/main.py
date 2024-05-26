# src/main.py

from switcher.switcher import ModuleSwitcher

def main():
    switcher = ModuleSwitcher()

    while True:
        print("Enter the module number to run (1: Face Recognition, 2: Object Detection, 3: Depth Sense, 4: OCR, 0: Exit):")
        try:
            module_number = int(input())
            if module_number == 0:
                print("Exiting...")
                switcher.switch_module(module_number, None)  # Stop any running thread
                break

            image = "sample_image.jpg"  # Replace with actual image path or input method
            switcher.switch_module(module_number, image)
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
