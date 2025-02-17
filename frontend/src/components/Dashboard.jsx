import React from 'react';
import QRCodeScanner from './QRCodeScanner';  // Assure-toi d'importer le bon chemin
import { logout } from '../api/auth';
import { useHistory } from 'react-router-dom';
import { getStudents, getStudent } from '../api/api';

const Dashboard = () => {
  const [students, setStudents] = useState([]);
  const history = useHistory();
  useEffect(() => {
    getStudents()
      .then((data) => {
        setStudents(data);  // Mettre à jour l'état avec la liste des étudiants récupérée
      })
      .catch((error) => {
        console.error('Erreur:', error);
      });
  }, []);

  const handleLogout = () => {
    logout();
    history.push('/login');  // Rediriger vers la page de connexion
  };
  return (
    <div>
      <h2>Dashboard</h2>
      <QRCodeScanner />
    </div>
  );
};

export default Dashboard;
