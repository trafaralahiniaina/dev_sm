import Link from "next/link";
import React from 'react';
import Signdialog_drawer from "./Signdialog_drawer";

interface NavigationItem {
  name: string;
  href: string;
  current: boolean;
}

const navigation: NavigationItem[] = [
  { name: 'Acceuil', href: '/', current: true },
  { name: 'Mentions', href: '', current: false },
  { name: 'Activités', href: '', current: false },
  { name: 'Conctact', href: '/contact', current: false },
  { name: 'A propos', href: '', current: false },
];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
}

const Data = () => {
  return (
    <div className="rounded-md max-w-sm w-full mx-auto">
      <div className="flex-1 space-y-4 py-1">
        <div className="sm:block">
          <div className="space-y-1 px-5 pt-2 pb-3">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={classNames(
                  item.current ? 'text-black hover:opacity-100' : 'hover:text-black hover:opacity-100',
                  'py-1 text-lg font-normal opacity-75 block'
                )}
                aria-current={item.current ? 'page' : undefined}
              >
                {item.name}
              </Link>
            ))}
            <div className="mt-4"></div>
              <Signdialog_drawer />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Data;
