<script>
  import {onMount} from 'svelte';
  import axios from 'axios';
  import io from 'socket.io-client';

  let messages = [];
  let newMessage = '';

  // 여기가 socket.io 연결하는 부분
  const socket = io("http://localhost:8000");

  onMount(async() =>{
    // 이 부분은 RestAPI 호출하는 부분
    const response = await axios('http://localhost:8000/messages');
    console.log(response.data[0]);
    messages = [...messages,...response.data];
    
    
    console.log(messages);


    //서버에서 호출하는 부분
    socket.on("message",(message)=>{
      messages =[...messages,message];
      newMessage = '';
      console.log(messages);
    })
  })

  function sendMessage(){
    const message = {
      text:newMessage,
      timestamp : new Date().toISOString(),
    }

    //axios.post('http://localhost:8000/post_messages',message);    //RestAPI 호출
    socket.emit('message',message);     // socket.io 호출

  }
</script>

<input bind:value={newMessage} on:keydown="{e=> e.key==='Enter' && sendMessage()}"/>
<button on:click={sendMessage}>Send</button>

<ul>
{#each messages as message (message.timestamp)}
<li>{new Date(message.timestamp).toLocaleTimeString()}: {message.text}</li>
{/each}
</ul>