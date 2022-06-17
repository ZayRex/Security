from sys import argv
from common import *
from const import *
import os

options = ['--relay', '--break-heart', '--custom']
if len(argv) > 1:
    if argv[1] in options:
        #init dialog and set a name for alice's buffer
        alice_buffer = 'aliceBuffer'
        dialog = Dialog('print')

        #impersonate Bob and secure a connection to Alice's socket
        bob = 'bob'
        alice_socket, alice_aes = setup(bob, BUFFER_DIR, BUFFER_FILE_NAME)
        os.rename(BUFFER_DIR+BUFFER_FILE_NAME, BUFFER_DIR+alice_buffer)
        dialog.think('Eve thinks:Nice, I have established a connection with alice')

        #impersonate Alice and secure a connection to Bob's socket
        alice = 'alice'
        bob_socket, bob_aes = setup(alice, BUFFER_DIR, BUFFER_FILE_NAME)
        dialog.think('Eve thinks:YESS, I have established a connection with bob as well')

        #recieve and decrypt message from Bob
        received_from_bob = receive_and_decrypt(bob_aes, bob_socket)
        dialog.chat('Bob said: "{}"'.format(received_from_bob))

        if argv[1] == options[0]:
            to_send = received_from_bob
        elif argv[1] == options[1]:
            to_send = BAD_MSG[bob]
        elif argv[1] == options[2]:
            CUSTOM_CHAT = True
            dialog.prompt('Type a message to Alice..')
            to_send = input()

        #encrypt and send a message to Alice
        encrypt_and_send(to_send, alice_aes, alice_socket)
        dialog.info('Message relayed! Waiting for reply...')

        #recieve and decrypt a message from Alice
        received_from_alice = receive_and_decrypt(alice_aes, alice_socket)
        dialog.chat('Alice said: "{}"'.format(received_from_alice))

        if argv[1] == options[0] or argv[1] == options[1]:
            to_send = received_from_alice
        elif argv[1] == options[2]:
            CUSTOM_CHAT = True
            dialog.prompt('Type a message to Bob..')
            to_send = input()

        #encrypt and send message to Bob
        encrypt_and_send(to_send, bob_aes, bob_socket)
        dialog.info('Message relayed! Waiting for reply...')

        #close both connection sockets
        tear_down(bob_socket, BUFFER_DIR, BUFFER_FILE_NAME)
        tear_down(alice_socket, BUFFER_DIR, alice_buffer)

