// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBt5H4XqY5Pfe_-aqfT95sNZryHHWLDlS0",
  authDomain: "respiretech-5da30.firebaseapp.com",
  projectId: "respiretech-5da30",
  storageBucket: "respiretech-5da30.appspot.com",
  messagingSenderId: "867880506669",
  appId: "1:867880506669:web:1a5706a290ca323cc66fa4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);