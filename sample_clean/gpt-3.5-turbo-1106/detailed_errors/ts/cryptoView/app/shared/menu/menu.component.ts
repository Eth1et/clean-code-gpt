import { Component, EventEmitter, Output, Input } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../models/User';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent {
  @Output() onCloseSidenav: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() onLogout: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Input() loggedInUser: User | null | undefined;

  constructor(private router: Router) {}

  close(logout?: boolean): void {
    this.onCloseSidenav.emit(true);
    if (logout) {
      this.onLogout.emit(true);
    }
  }
}