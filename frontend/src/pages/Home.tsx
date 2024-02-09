import { Button } from '@/components/ui/button'
import { useQuery } from '@tanstack/react-query'

const Home = () => {
	const { data } = useQuery({
		queryKey: ['HelloWorld'],
		queryFn: async () => {
			const response = await fetch(import.meta.env.VITE_BACKEND_URL)
			const data = await response.json()
			return data
		},
	})

	console.log(data)

	return (
		<div>
			<Button>Hello there</Button>
		</div>
	)
}

export default Home
