from dotenv import load_dotenv
from BusinessLogic.notification_business_logic import NotificationBusinessLogic
from Common.Services.notification_consumer import NotificationConsumer

load_dotenv()

business_logic = NotificationBusinessLogic()
consumer = NotificationConsumer(business_logic.process)
consumer.start()