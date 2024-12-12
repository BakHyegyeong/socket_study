const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const bodyParser= require('body-parser');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());     // body
app.use(cors());        // cors 부분 에러 해결, 모든 도메인에서의 요청 허용
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
      origin: "*",
      methods: ["GET", "POST"]
    }
    });

let messages = [{text: '어서오세요!', timestamp : new Date().toISOString()}];  //메세지들을 저장할 배열


app.get('/messages',( req,res)=>{
    console.log("이전 메시지들을 불러옵니다.")
    req.json(messages);
})

//메시지 전송예시 1 - RestAPI
app.post('/post_messages',(req,res)=>{
    const reqMessage = req.body;
    //messages.push(reqMessage);

    io.emit('message',reqMessage);
    
    res.status(201).end();
})

io.on('connection',(socket) => {
    console.log('New Client Connected');

    // 메시지 전송예시 2 - socket.io
    socket.on('message',(reqMessage) =>{
        messages.push(reqMessage);
        io.emit('message',reqMessage);  // client측에서 정의된 message이벤트를 실행
    });

    socket.on('disconnect',() =>{
        console.log('Client disconnect');
    });
});

server.listen(8000,() => console.log('Listening on port 8000'));