// import { NextResponse } from 'next/server'
// import type { NextRequest } from 'next/server'
// import schools from './schools.json'

// export function middleware(request: NextRequest) {
//   const url = request.nextUrl.clone()
//   const hostname = request.headers.get('host') || ''

//   const subdomain = hostname.split('.')[0]

//   const school = schools.find(school => school.subdomain === subdomain)

//   if (school) {
//     url.pathname = `/school/${school.slug}/${school.id}${url.pathname}`
//   } else {
//     url.pathname = `/${url.pathname}`
//   }

//   return NextResponse.rewrite(url)
// }

// export const config = {
//   matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
// }

// import { NextResponse } from 'next/server'
// import type { NextRequest } from 'next/server'
// import schools from './schools.json'

// export function middleware(request: NextRequest) {
//   // Votre logique de middleware ici
//   return NextResponse.next()
// }

// export const config = {
//   matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
// }


// import { NextResponse } from 'next/server'
// import type { NextRequest } from 'next/server'
// import schools from './data/schools.json'

// export function middleware(request: NextRequest) {
//   const url = request.nextUrl.clone()
//   const hostname = request.headers.get('host') || ''

//   const subdomain = hostname.split('.')[0]

//   const school = schools.find(school => school.subdomain === subdomain)

//   if (school) {
//     url.pathname = `/school/${school.id}${url.pathname}`
//   } else {
//     url.pathname = `/${url.pathname}`
//   }

//   return NextResponse.rewrite(url)
// }

// export const config = {
//   matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
// }

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import schools from './data/schools.json'

export function middleware(request: NextRequest) {
  const url = request.nextUrl.clone()
  const hostname = request.headers.get('host') || ''

  const school = schools.find(school => school.website.includes(hostname))

  if (school) {
    url.pathname = `/school/${school.id}${url.pathname}`
  } else {
    url.pathname = `/${url.pathname}`
  }

  return NextResponse.rewrite(url)
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}