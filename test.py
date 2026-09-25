
from create.transactions import submitTransactionsToDB
from create.users import createNewUser
from read.users import getUserId
from read.transactions import getTransactions

def test():
    return getUserId("test@example.com", "password123");