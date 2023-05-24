// Retrieve a JSON file every some time, and fill in a <div> element with it
//

function getMessages (url, container) {
  fetch(url).then(response => {
    console.log("Response received!", response)
    if (!response.ok) {
      throw new Error("HTTP error " + response.status);
    }
    return response.json();
 }).then(messages => {
    console.log(messages);
    messages_str = ""
    messages.forEach(message => {
      message_str = "<p>"

      if (message.isimg) {
        message_str += `<img src=${message.text}>`
      } else {
        message_str += message.text
      }
      message_str += `<br/>Author: ${message.author}</p>`

      messages_str += message_str
    });
    container.innerHTML = messages_str;
 }).catch(function () {
    console.log("Error decoding JSON")
 })
}

window.addEventListener("DOMContentLoaded", (event) => {
  console.log("DOM fully loaded and parsed");
  const container = document.querySelector('#messages');
  getMessages(url_messages, container);
  setInterval(() => {
    console.log("Interval");
    getMessages(url_messages, container);
    }, 10 * 1000); // Call every 10 seconds
});
