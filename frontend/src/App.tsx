import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Home } from './pages/Home'

const queryClient = new QueryClient()

function App() {
	document.body.classList.add('dark')
	return (
		<QueryClientProvider client={queryClient}>
			<Home />
		</QueryClientProvider>
	)
}

export default App
