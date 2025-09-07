import React from "react";
import { useState } from "react";

const initialFriends = [
  {
    id: 118836,
    name: "Clark",
    image: "https://i.pravatar.cc/48?u=118836",
    balance: -7,
  },
  {
    id: 933372,
    name: "Sarah",
    image: "https://i.pravatar.cc/48?u=933372",
    balance: 20,
  },
  {
    id: 499476,
    name: "Anthony",
    image: "https://i.pravatar.cc/48?u=499476",
    balance: 0,
  },
];

function Button({ children, onClick }) {
  return <button className="button" onClick={onClick}>{children}</button>;
}

const App = () => {

  const [friends, setFriends] = useState(initialFriends)
  const [showAddFriend, setShowAddFriend] = useState(false);
  const [selectedFriend, setSelectedFriend] = useState(null)

  function handelShowAddFriend() {
    setShowAddFriend((show) => !show)
  }

  function handelAddFriend(friend) {
    setFriends(friends => [...friends, friend]);
    setShowAddFriend(false);
  }

  function handelSelection(friend) {
    // setSelectedFriend(friend);
    setSelectedFriend((cur) => cur?.id === friend.id ? null : friend);
    setShowAddFriend(false)

  }
  return (
    <div className="app">
      <div className="sidebar">
        <FriendsList friends={friends} onSelection={handelSelection} selectedFriend={selectedFriend} />
        {showAddFriend && <FormAddFriend onAddFriend={handelAddFriend} />}
        <Button onClick={handelShowAddFriend}>{showAddFriend ? 'Close' : "Add friend"}</Button>
      </div>
      {selectedFriend && <FormSplitBill selectedFriend={selectedFriend} />}
    </div>
  );
};

function FriendsList({ friends, onSelection, selectedFriend }) {
  return (
    <ul>
      {friends.map((friend) => (
        <Friend friend={friend} key={friend.id} selectedFriend={selectedFriend} onSelection={onSelection} />
      ))}
    </ul>
  );
}

function Friend({ friend, onSelection, selectedFriend }) {

  const isSelected = selectedFriend?.id === friend.id;

  return (
    <li className={isSelected ? "selected" : ""}>
      <img src={friend.image} alt={friend.name} />
      <h3>{friend.name}</h3>
      {friend.balance < 0 && (
        <p className="red">
          You owe {friend.name} ${Math.abs(friend.balance)}
        </p>
      )}
      {friend.balance > 0 && (
        <p className="green">
          {friend.name} owe you ${Math.abs(friend.balance)}
        </p>
      )}
      {friend.balance === 0 && (
        <p>
          You and {friend.name} ${Math.abs(friend.balance)} are even
        </p>
      )}
      <Button onClick={() => onSelection(friend)}>{isSelected ? "Close" : "Select"}</Button>
    </li>
  );
}



function FormAddFriend({ onAddFriend }) {

  const [name, setName] = useState("");
  const [image, setImage] = useState("https://i.pravatar.cc/48");

  function handelSubmit(e) {
    e.preventDefault();

    if (!name || !image) return;
    const id = crypto.randomUUID();
    const newFriend = {
      id,
      name,
      image: `${image}?=${id}`,
      balance: 0,
    };
    onAddFriend(newFriend);
    console.log(newFriend);

    setName('');
    setImage('https://i.pravatar.cc/48')

  }
  return (
    <form className="form-add-friend" onSubmit={handelSubmit}>
      <label>👥Friend name</label>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)} />
      <label htmlFor=""> 🌄 Image URL</label>
      <input
        type="text"
        value={image}
        onChange={(e) => setImage(e.target.value)} />
      <Button>Add</Button>
    </form>
  );
}

function FormSplitBill({ selectedFriend }) {

  const [bill, setBill] = useState("");
  const [paidByUser, setPaidByUser] = useState("");
  const [whoIsPaying, setWhoIsPaying] = useState('user')
  return <form className="form-split-bill">
    <h2>Split a bill with {selectedFriend.name}</h2>
    <label>💷Bill value</label>
    <input type="text" value={bill} onChange={(e) => setBill(Number(e.target.value))} />
    <label>👤Your expense</label>
    <input type="text" value={paidByUser} onChange={(e) => setPaidByUser(Number(e.target.value))} />
    <label>👯‍♀️{selectedFriend.name}'s expense</label>
    <input type="text" disabled />

    <label>🤑 Who is paying the bill</label>
    <select
      value={whoIsPaying} onChange={(e) => setWhoIsPaying((e) => e.target.value)}
    >
      <option value="user">You</option>
      <option value="friend">{selectedFriend.name}</option>
    </select>

    <Button>Split Bill</Button>
  </form>
}

export default App;
