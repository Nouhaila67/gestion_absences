import React, { useState } from 'react';
import { QRCodeReader } from 'react-qr-reader';
import axios from 'axios';

const QRCodeScanner = () => {
  const [scannedData, setScannedData] = useState(null);
  const [courseName, setCourseName] = useState('');

  const handleScan = async (data) => {
    if (data) {
      setScannedData(data);

      const studentId = data.split(":")[1];  // Assurez-vous que le QR code est bien formaté comme ID:12345

      try {
        await axios.post('http://localhost:8000/register-presence/', {
          student_id: studentId,
          course_name: courseName,
        });
        alert('Presence registered successfully');
      } catch (error) {
        alert('Error registering presence');
      }
    }
  };

  const handleError = (err) => {
    console.error(err);
  };

  return (
    <div>
      <QRCodeReader
        delay={300}
        onScan={handleScan}
        onError={handleError}
      />
      <input
        type="text"
        placeholder="Enter course name"
        value={courseName}
        onChange={(e) => setCourseName(e.target.value)}
      />
      {scannedData && <p>Scanned Data: {scannedData}</p>}
    </div>
  );
};

export default QRCodeScanner;
