import logging
from app.commands import Command
from create_database import main

class CreateDatabase(Command):
    def __init__(self):
        super().__init__()
        self.name = "create_database"
        self.description = "This agent creates and stores the downloaded github files into a local database."
        self.history = []

    def execute(self, *args, **kwargs):
        character_name = kwargs.get("character_name", "Create Database")
        print(f"Database is being created...")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "done":
                print("Goodbye.")
                break

            if user_input.lower() == "run" :
                main()

            self.history.append(("user", user_input))
            
            try:
                response, tokens_used = self.interact_with_ai(user_input, character_name)
                print(f"Movie Expert: {response}")
                print(f"(This interaction used {tokens_used} tokens.)")
                self.history.append(("system", response))
            except Exception as e:
                print("Sorry, there was an error processing your request. Please try again.")
                logging.error(f"Error during interaction: {e}")
