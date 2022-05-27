from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot(
  'CoronaBot',
  secret_key='12345678-1234-1234-1234-123456789012',
  storage_adapter='chatterbot.storage.SQLStorageAdapter',
  logic_adapters=[
    {
      'import_path': 'adapter_sede.adapter_sede'
    },
    {
      'import_path': 'chatterbot.logic.BestMatch',
      'default_response': 'Scusa, ma non riesco a capire. Sto imparando.',
      'maximum_similarity_threshold': 0.90
    }
  ],
)

 # Training with Personal Ques & Ans 
training_data_simple = open('training_data/simple.txt').read().splitlines()

trainer = ListTrainer(chatbot)
trainer.train(training_data_simple)

# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)