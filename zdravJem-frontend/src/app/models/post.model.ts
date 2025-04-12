export interface Post {
  id?: string; // Firestore will auto-generate this
  author: string;
  content?: string;
  imageUrl?: string;
  emoji?: string;
  timestamp: Date;
}
