import { Component, EventEmitter, Output, Input } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../models/User';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent {
  @Output() closeSidenav = new EventEmitter<void>();
  @Output() logout = new EventEmitter<void>();
  @Input() currentUser: User | null = null;

  constructor(private router: Router) {}

  handleCloseSidenav(shouldLogout: boolean = false) {
    this.closeSidenav.emit();
    if (shouldLogout) {
      this.logout.emit();
    }
  }
}