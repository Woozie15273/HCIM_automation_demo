from src.core.main_app import MainApp

if __name__ == "__main__":
    app = MainApp()
    try:
        app.run()
    finally:
        app.teardown()
