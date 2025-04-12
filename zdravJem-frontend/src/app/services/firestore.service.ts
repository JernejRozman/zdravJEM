import { Injectable } from '@angular/core';
import { Firestore, collection, addDoc, collectionData } from '@angular/fire/firestore';
import { Post } from '../models/post.model';
import { CollectionReference, DocumentData } from 'firebase/firestore';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FirestoreService {
  private postsCollection: CollectionReference<DocumentData>;

  constructor(private firestore: Firestore) {
    this.postsCollection = collection(this.firestore, 'posts');
  }

  // Save a post
  async addPost(post: Post): Promise<void> {
    await addDoc(this.postsCollection, post);
    console.log('✅ Post added to Firestore');
  }

  // Get posts in realtime
  getPosts(): Observable<Post[]> {
    return collectionData(this.postsCollection, { idField: 'id' }) as Observable<Post[]>;
  }
}
