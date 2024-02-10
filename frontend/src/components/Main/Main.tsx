import { fetchAnalytics } from '@/lib/api/fetchAnalytics'
import { TabsContent } from '@radix-ui/react-tabs'
import { useSuspenseQuery } from '@tanstack/react-query'
import { SearchFormValues } from '../Header/Header'
import { Tabs, TabsList, TabsTrigger } from '../ui/tabs'
import Charts from './Charts'
import Feed from './Feed/Feed'

type Props = {
	searchValues: SearchFormValues | undefined
}

const Main = ({ searchValues }: Props) => {
	if (!searchValues) {
		return null
	}

	const { data, isError } = useSuspenseQuery({
		queryKey: ['search', searchValues!],
		queryFn: fetchAnalytics,
		refetchOnWindowFocus: false,
	})

	if (isError) {
		return <div>Error</div>
	}

	return (
		<div className='lg:max-w-[1200px] h-full px-16 mx-auto mt-4 mb-16'>
			<Tabs
				defaultValue='feed'
				className='flex justify-center flex-col items-center space-y-8'
			>
				<TabsList>
					<TabsTrigger value='feed'>Feed</TabsTrigger>
					<TabsTrigger value='charts'>Analytics</TabsTrigger>
				</TabsList>

				<TabsContent value='feed'>
					<Feed posts={data.posts} />
				</TabsContent>
				<TabsContent value='charts'>
					<Charts />
				</TabsContent>
			</Tabs>
		</div>
	)
}

export default Main
