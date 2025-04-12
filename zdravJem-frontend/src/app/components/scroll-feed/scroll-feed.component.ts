import { Component, OnInit } from '@angular/core';
import { FirestoreService } from '../../services/firestore.service';
import { Post } from '../../models/post.model';

@Component({
  selector: 'app-scroll-feed',
  standalone: false,
  templateUrl: './scroll-feed.component.html',
  styleUrls: ['./scroll-feed.component.css']
})
export class ScrollFeedComponent implements OnInit {
  posts: Post[] = [];

  constructor(private firestoreService: FirestoreService) {}

  ngOnInit(): void {
    this.firestoreService.getPosts().subscribe((data) => {
      // Optional: sort by date (most recent first)
      //this.posts = data.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
    });
  }

  handleReaction(event: Event): void {
    const target = event.target as HTMLElement;
    target.classList.add('active');
    setTimeout(() => {
      target.classList.remove('active');
    }, 300);
  }
}
