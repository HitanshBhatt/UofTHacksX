// $(".person").on('click', function(){
//     $(this).toggleClass('focus').siblings().removeClass('focus');
//  })


class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox__messages'),
            sendButton: document.querySelector('.send__button')
        }
        this.messages = [];
    }

    display() {
        const { chatBox, sendButton } = this.args;
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))
        const node = document.querySelector('.bottom-bar').querySelector('input');
        console.log("Added key up listener", node)
        node.addEventListener("keyup", (event) => {
            console.log("key");
            if (event.key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    onSendButton(chatbox) {
        var textField = document.querySelector('div.bottom-bar input');
        let text1 = textField.value
        console.log(text1)
        if (text1 === "") {
            return;
        }
        let msg1 = { name: "user", message: text1 }
        this.messages.push(msg1);

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
                let msg2 = { name: "bot", data: r.answer };
                console.log(msg2)
                this.messages.push(msg2);
                this.updateChatText(chatbox)
                textField.value = ''

            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox)
                textField.value = ''
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
                    html += `<div class="bubble chatbox__link"><a href=${i.link} target="_blank">${i.name}<image href="static/link-solid.svg" width="1.25em"
                    height="1.25em" /></a><p>${i.description}</p></div>`
                }
                html += '</div>'
            }
        });
        chatbox.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display()
