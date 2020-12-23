from postman import PostMan

if __name__ == '__main__':
    postman = PostMan('login@gmail.com', 'qwerty')
    postman.mail_send('Subject', ['vasya@email.com', 'petya@email.com'], 'Message')
    print(postman.mail_receive())
