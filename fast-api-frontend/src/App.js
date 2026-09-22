import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [user, setUser] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [editUserId, setEditUserId] = useState(null);
  const API_URL = 'http://localhost:8000/users/';

  //Fetch all users from the database(GET)
  const fetchUsers = async () => {
    try {
      const response = await fetch(API_URL);
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      const data = await response.json();
      setUser(data);
    } catch (error) {
      setError(error.message);
    }

  };
  useEffect(() => {
    fetchUsers();
  }, []);

  //Add a new user to the database(POST)
  const addUser = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email })
      });
      if (!response.ok) {
        throw new Error('Failed to add user');
      }

      setEmail('');
      setName('');
      fetchUsers();  //refresh the list of users after adding a new user
    } catch (error) {
      setError(error.message);
    }
  };
  //populate the form with the user data to be edited
  const editUser = (user) => {
    setEditUserId(user.id);
    setName(user.name);
    setEmail(user.email);
  };
  //submit the updated user data to the database(PUT)
  const updateUser = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch(`${API_URL}${editUserId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email })
      });
      if (!response.ok) {
        throw new Error('Failed to update user');
      }
      setEditUserId(null);
      setEmail('');
      setName('');
      fetchUsers();  //refresh the list of users after updating a user
    } catch (error) {
      setError(error.message);
    }
  };
  //Remove a user from the database(DELETE)
  const removeUser = async (id) => {
    setError('');
    try {
      const response = await fetch(`${API_URL}${id}`, {
        method: 'DELETE'
      });
      if (!response.ok) {
        throw new Error('Failed to delete user');

      }
      fetchUsers();  //refresh the list of users after deleting a user
    } catch (error) {
      setError(error.message);
    }
  };
  return (
    <div style={{ padding: '40px', maxWidth: '600px', margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Database User Management</h1>
      {error && <p style={{ color: 'red', backgroundColor: 'lightgray', padding: '10px', borderRadius: '5px' }}>{error}</p>}
      <form onSubmit={editUserId ? updateUser : addUser} style={{ marginBottom: '20px', display: 'flex', flexDirection: 'column' }}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ marginBottom: '10px', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ marginBottom: '10px', padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
        />
        <div style={{ display: 'flex', gap: '10px' }}>
          <button type="submit" style={{ padding: '10px', flex: 1, cursor: 'pointer', borderRadius: '5px', backgroundColor: editUserId ? '#28a745' : '#007BFF', color: editUserId ? '#fff' : '#fff', border: 'none' }}>
            {editUserId ? 'Update User' : 'Add User'}
          </button>
          {editUserId && (
            <button type="button" onClick={() => { setEditUserId(null); setName(''); setEmail(''); }} style={{ padding: '10px', flex: 1, cursor: 'pointer', borderRadius: '5px', backgroundColor: '#6c757d', color: '#fff', border: 'none' }}>
              Cancel
            </button>
          )}
        </div>
      </form>
      {/* Profile of users in the database */}
      <h2>Saved Users Profile({user.length})</h2>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {user.map((u) => (
          <li key={u.id} style={{ marginBottom: '10px', padding: '10px', borderRadius: '5px', backgroundColor: '#f9f9f9', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>{u.name} ({u.email})</span>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button onClick={() => editUser(u)} style={{ padding: '5px 10px', borderRadius: '5px', backgroundColor: '#007BFF', color: '#fff', border: 'none' }}>Edit</button>



              <button onClick={() => removeUser(u.id)} style={{ padding: '5px 10px', borderRadius: '5px', backgroundColor: '#dc3545', color: '#fff', border: 'none' }}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;   