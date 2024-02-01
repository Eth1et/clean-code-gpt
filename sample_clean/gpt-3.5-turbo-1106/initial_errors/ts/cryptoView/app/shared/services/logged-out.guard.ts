@Injectable({
  providedIn: 'root'
})
export class LoggedOutGuard implements CanActivate {

  constructor(private router: Router){}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean | UrlTree {
    const user = JSON.parse(localStorage.getItem('user') || '{}') as User;
    
    if (user) {
      return this.router.parseUrl('main');
    }
    
    return true;
  }
}