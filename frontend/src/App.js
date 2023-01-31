import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import ReactPlayer from 'react-player';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Typewriter } from 'react-simple-typewriter';

const App = () => {

  const [conversationId, setConversationId] = useState(null);
  const [getLoading, setGetLoading] = useState(true);
  const [error, setError] = useState(null);
  const [question, setQuestion] = useState('');
  const [typeQuestion, setTypeQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [ansLoading, setAnsLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://172.20.10.2:8080/generateConversationId${window.location.pathname}`);
        setConversationId(response.data.message);
      } catch (err) {
        setError(err);
        alert(error);
      } finally {
        setGetLoading(false);
      }
    };
    fetchData();
  }, []);

  const playerRef = useRef(null);
  const onSeek = (time) => {
    playerRef.current.seekTo(time);
  }

  const sendQuestion = async (e) => {
    e.preventDefault();
    setAnsLoading(true);
    setTypeQuestion(`Question: ${question}`);
    if (question.toLowerCase().startsWith("where did")){
      try {
        const response = await axios.get(`http://172.20.10.2:8080/extractRecentPercentage/${conversationId}`);
        onSeek(response.data.percent);
      } catch (err) {
        alert('Error getting seek: ' + err);
      } finally {
        setAnsLoading(false);
        setQuestion('');
      }
    } else{
      try {
        const response = await axios.post(`http://172.20.10.2:8080/askQuestion/${conversationId}`, {'question': question});
        setAnswer(`Answer: ${response.data.message}`);
      } catch (err) {
        alert('Error sending question: ' + err);
      } finally {
        setAnsLoading(false);
        setQuestion('');
      }
    }
  };

  return (
    <div className='flex flex-col justify-start items-center p-5 h-screen bg-black'>
      <div className='flex flex-row justify-around items-center p-5 my-5 rounded-lg w-full bg-gray-500'>
        {!getLoading && <ReactPlayer url={`http://172.20.10.2:8080/lectures${window.location.pathname}.mp4`} width="640px" height="350px" playing={true} muted={true} controls={true} ref={playerRef} />}
        <div className='flex flex-col w-1/2 justify-between items-center h-full ml-5'>
          <div className='flex w-full rounded-lg p-3 bg-gray-200 h-1/4 overflow-y-auto'>{typeQuestion}</div>
          <div className='flex w-full rounded-lg p-3 bg-gray-200 h-2/3 overflow-y-auto'>
            {ansLoading ? <div>hold on, let me think...</div> : (answer && <Typewriter typeSpeed={30} words={[answer]}/>)}
          </div>
        </div>
      </div>
      <form onSubmit={sendQuestion} className='flex justify-between w-full'>
        <input value={question} type='text' placeholder='Ask a question...' onChange={(e) => setQuestion(e.target.value)} className='bg-gray-200 p-2 rounded-lg w-full' />
      </form>
    </div>
  );
}

export default App;
