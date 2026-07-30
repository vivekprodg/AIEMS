import { redirect } from 'next/navigation';

export default function App() {
  // Instant Server-Side Redirect to /home
  redirect('/home');
}