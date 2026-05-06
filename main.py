import sys
from PySide6.QtWidgets import QApplication
from src.gui.main_window import AegisVaultApp
from src.utils.logger import logger

def main():
    try:
        logger.info("Initializing AegisVault...")
        app = QApplication(sys.argv)
        
        # Set app-wide metadata
        app.setApplicationName("AegisVault")
        app.setOrganizationName("AntigravitySoft")
        
        window = AegisVaultApp()
        window.show()
        
        logger.info("AegisVault GUI Started Successfully.")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Fatal error during initialization: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
