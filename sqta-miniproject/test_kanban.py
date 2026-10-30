import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KanbanBoardRegressionTests(unittest.TestCase):

    def setUp(self):
        # Launches a new clean Chrome window
        self.driver = webdriver.Chrome()
        
        # ⚠️ CHANGE THIS: Paste your exact file path copied from Step 2 here!
        self.local_file_path = "file:///C:/Users/YourName/Desktop/index.html"
        
        self.driver.get("file:///C:/Users/hp/Desktop/index.html")
        self.driver.implicitly_wait(5)

    def test_add_and_delete_task_flow(self):
        driver = self.driver
        
        # 1. Locate UI elements by their structural IDs
        title_input = driver.find_element(By.ID, "task-title")
        add_button = driver.find_element(By.ID, "btn-add-task")
        
        # 2. Execute Action: Type a task title and click Add
        test_title = "Automated Regression Task"
        title_input.send_keys(test_title)
        add_button.click()
        
        # 3. Verify: Check if the task text appeared inside the 'To Do' column
        task_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@id='todo-col']//p[text()='{test_title}']"))
        )
        self.assertTrue(task_element.is_displayed(), "The task card was not successfully added to the DOM.")
        
        # 4. Execute Action: Locate and click the 'Delete' button on that specific card
        delete_btn = driver.find_element(By.XPATH, f"//p[text()='{test_title}']/following-sibling::div/button[text()='Delete']")
        delete_btn.click()
        
        # 5. Verify: Check that the task card completely disappears from the screen
        is_removed = WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.XPATH, f"//p[text()='{test_title}']"))
        )
        self.assertTrue(is_removed, "The task card was not removed from the screen after clicking delete.")

    def tearDown(self):
        # Closes the Chrome window automatically when finished
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
