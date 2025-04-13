// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCUWNEQMFhoZFqgRyf62UYJTvfPJmH-u_A",
  authDomain: "zdravjem-b86fd.firebaseapp.com",
  projectId: "zdravjem-b86fd",
  storageBucket: "zdravjem-b86fd.firebasestorage.app",
  messagingSenderId: "965525541183",
  appId: "1:965525541183:web:44b4bbd8c335b30b50c38a",
  measurementId: "G-JR89TKZNG3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
