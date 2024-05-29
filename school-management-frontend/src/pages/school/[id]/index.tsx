import { GetServerSideProps } from 'next'
import axios from 'axios'
import Layout from '@/components/Layout'
import { School } from '@/types/school'

interface SchoolProps {
  schoolData: School
}

const SchoolPage: React.FC<SchoolProps> = ({ schoolData }) => {
  return (
    <Layout school={schoolData}>
      <div>
        <h1>{schoolData.name}</h1>
        <p>{schoolData.slogan}</p>
        {/* Ajoutez le contenu spécifique à la page d'accueil */}
      </div>
    </Layout>
  )
}

export const getServerSideProps: GetServerSideProps<SchoolProps> = async ({ params }) => {
  const { id } = params || {}

  try {
    const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/schools/${id}/`)

    const schoolData = response.data

    if (!schoolData) {
      return {
        notFound: true,
      }
    }

    return {
      props: {
        schoolData,
      },
    }
  } catch (error) {
    console.error('Error fetching school data:', error)
    return {
      notFound: true,
    }
  }
}

export default SchoolPage