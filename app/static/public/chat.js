const socketio = io();

const messages = document.getElementById("messages");

socketio.on("message", (response) => {
  const message = response.owner === "bot" ? `
  <div class="flex items-center space-x-3">
    <div>
      <img
        src="${response.botData.picture}"
        alt="${response.botData.name}"
        class="rounded-full w-11"
      />
    </div>
    <div class="bg-chatbg rounded-3xl p-6 w-fit">
      ${response.data}
    </div>
  </div>
  ` : `
  <div class="ml-auto space-x-3">
    <div class="w-11"></div>
    <div class="bg-cardbg rounded-3xl p-6 w-fit">
      ${response.data}
    </div>
  </div>
  `
  messages.innerHTML += message;
});

const sendMessage = (event) => {
  event.preventDefault();
  const message = document.getElementById("message");
  socketio.emit("message", { data: message.value });
  message.value = "";
};
