// src/app/main/page.tsx
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default function MainHome() {
  const schoolDomain = 'i-anatra'
  const slogan = 'Apprendre pour un avenir meilleur'
  const menuItems = [
    { label: 'Accueil', link: '' },
    { label: 'À propos', link: 'about' },
    { label: 'Contact', link: 'contact' },
  ]

  return (
    <div>
      <Header schoolDomain={schoolDomain} menuItems={menuItems} slogan={slogan} />
      <main className="p-4">
        <h1>Bienvenue sur la plateforme i-anatra</h1>
        <p>
          Cette plateforme offre un espace unifié pour la gestion des écoles et des étudiants, tout en permettant à chaque établissement d'avoir sa propre identité.
        </p>
      </main>
      <Footer schoolDomain={schoolDomain} address="123 Avenue de l'Éducation, Antananarivo" />
    </div>
  )
}