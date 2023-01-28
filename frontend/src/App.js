import React, { useEffect, useState } from 'react';
import YouTube from 'react-youtube';
import axios from 'axios';

const testVid = {
  id: 'alJaltUmrGo',
  url: 'https://www.youtube.com/watch?v=alJaltUmrGo',
}

const App = () => {

  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [question, setQuestion] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://hackbrown.ngrok.io/generateConversationId/temp');
        setConversationId(response.data.message);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const opts = {
    height: '390',
    width: '640',
    playerVars: {
      autoplay: 1,
    },
  };

  const onPlayerReady = (event) => {
    event.target.pauseVideo();
  }

  const onChange = (e) => {
    setQuestion(e.target.value);
  }

  const sendQuestion = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`http://hackbrown.ngrok.io/askQuestion/temp${conversationId}`, question);
      alert('Question sent successfully!');
    } catch (err) {
      alert('Error sending question: ' + err);
    }
  };
  
  return (
    <div className='flex flex-col justify-start items-center p-5 h-screen bg-black'>
      <h1 className='text-3xl font-bold Interpreter text-white'>Smart Video</h1>
      <div className='flex flex-row p-5 my-5 rounded-lg w-full bg-gray-500'>
        {!loading && <YouTube videoId={testVid.id} opts={opts} onReady={onPlayerReady} />}
      </div>
      <form onSubmit={sendQuestion} className='flex justify-between w-full'>
        <input type='text' placeholder='Search' onChange={(e) => onChange(e)} className='bg-gray-200 p-2 rounded-lg w-11/12' />
        <input type='submit' value='Search' className='flex justify-center items-center px-5 py-1 cursor-pointer rounded-lg bg-emerald-400 hover:bg-emerald-200 font-bold text-white' />
      </form>
    </div>
  );
}

export default App;
