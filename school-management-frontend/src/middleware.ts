// middleware.ts
/* import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { fetchSchoolBySigle } from './lib/api';

export async function middleware(req: NextRequest) {
  const url = req.nextUrl.clone();
  const host = req.headers.get('host') || '';
  const schoolDomain = host.split('.')[0];

  // Ne pas rediriger les ressources statiques et les fichiers internes de Next.js
  const isPublicFile = /\.(.*)$/.test(url.pathname) || ['/favicon.ico', '/robots.txt', '/_next', '/static'].some(path => url.pathname.startsWith(path));
  
  const isSchoolDomain = await fetchSchoolBySigle(schoolDomain);


  
  // If it's not a public file and we have a valid school domain
  if (!isPublicFile && isSchoolDomain && schoolDomain !== 'localhost:3000') {
    url.pathname = `${schoolDomain}${url.pathname}`;
    return NextResponse.rewrite(url);
  }
 
return NextResponse.next();
} */

// middleware.ts

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { fetchSchoolBySigle } from './lib/api';

export async function middleware(req: NextRequest) {
  const url = req.nextUrl.clone();
  const host = req.headers.get('host') || '';
  const schoolDomain = host.split('.')[0];

  // Ne pas rediriger les ressources statiques et les fichiers internes de Next.js
  const isPublicFile = /\.(.*)$/.test(url.pathname) || ['/favicon.ico', '/robots.txt', '/_next', '/static'].some(path => url.pathname.startsWith(path));

  const school = await fetchSchoolBySigle(schoolDomain);

  // If it's not a public file and we have a valid school domain
  if (!isPublicFile && school && schoolDomain !== 'localhost:3000') {
    url.pathname = `${schoolDomain}${url.pathname}`;
    return NextResponse.rewrite(url);
  }

  return NextResponse.next();
}