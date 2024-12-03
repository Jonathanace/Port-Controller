// frontend/components/MessageComponent.tsx

import { useEffect, useState } from 'react';

const MessageComponent: React.FC = () => {
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching data...');
        const response = await fetch('http://localhost:5328/api/hello');
        console.log('Response:', response);
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.text();
        console.log('Result:', result);
        setMessage(result);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Message from Flask API</h1>
      <p>{message}</p>
    </div>
  );
};

export default MessageComponent;
