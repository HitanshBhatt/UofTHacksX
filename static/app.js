// $(".person").on('click', function(){
//     $(this).toggleClass('focus').siblings().removeClass('focus');
//  })


class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox__messages'),
            sendButton: document.querySelector('.send__button')
        }
        this.messages = [{ name: 'bot', data: [{ 'url-type': 'plain', text: 'What can the MentalBase bot help you with today?' }] }];
        this.updateChatText(document.querySelector('.chatbox__messages'))
    }

    display() {
        const { chatBox, sendButton } = this.args;
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))
        const node = document.querySelector('.bottom-bar').querySelector('input');
        node.addEventListener("keyup", (event) => {
            if (event.key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
        const elipse = document.querySelector('div.waiting');
        elipse.style.display = 'none';
    }

    onSendButton(chatbox) {
        var textField = document.querySelector('div.bottom-bar input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }
        let msg1 = { name: "user", message: text1 }
        this.messages.push(msg1);
        this.updateChatText(chatbox)
        textField.value = ''
        const elipse = document.querySelector('div.waiting');
        elipse.style.display = 'block';
        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(r => r.json())
            .then(r => {
                const elipse = document.querySelector('div.waiting');
                elipse.style.display = 'none';
                let msg2 = { name: "bot", type: 'data', data: r.answer };
                this.messages.push(msg2);
                this.updateChatText(chatbox);

            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox);
            });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().forEach(function (item,) {
            if (item.name === "user") {
                html += '<div class="typing"><div class="bubble">' + item.message + '</div></div>'
            }
            else {
                html += `<div class="incoming">`
                for (const i of item.data) {
                    if (i['url-type'] == 'plain') {
                        html += `<div class="incoming"><div class="bubble">${i.text}</div></div>`
                    } else {
                        html += `<div class="bubble chatbox__link"><strong>${i['url-type'].charAt(0).toUpperCase() + i['url-type'].slice(1) + ': '} </strong><a href=${i.link} target="_blank">${i.name}<image href="static/link-solid.svg" width="1.25em"
                    height="1.25em" /></a><p>${i.description}</p></div>`
                    }
                }
                html += '</div>'
            }
        });
        chatbox.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display()
