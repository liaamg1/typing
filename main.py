"""Main fil till analyzer funktionerna"""
import typingfunctions
def main():
    """main kod"""
    stop = False
    while not stop:
        print("Choose an option:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Score")
        print("5. Train")
        print("q. Quit")
        
        choice = input("Enter your choice: ").lower()

        if choice == '1':
            easy = 'easy.txt'
            typingfunctions.difficulty(easy)
        elif choice == '2':
            medium = 'medium.txt'
            typingfunctions.difficulty(medium)
        elif choice == '3':
            hard = 'hard.txt'
            typingfunctions.difficulty(hard)
        elif choice == '4':
            typingfunctions.view_score()
        elif choice == '5':
            try:
                user_choice = int(input("How many seconds do you want to train? "))
                typingfunctions.train(user_choice)
            except ValueError:
                print("Error: Please enter a valid integer for the duration.")
        elif choice == 'q':
            stop = True
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
