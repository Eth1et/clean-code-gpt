import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

const bootstrapPromise = platformBrowserDynamic().bootstrapModule(AppModule);

bootstrapPromise.catch(error => console.error('Angular bootstrapping error:', error));