import { fetchAnalytics } from '@/lib/api/fetchAnalytics'
import { TabsContent } from '@radix-ui/react-tabs'
import { useSuspenseQuery } from '@tanstack/react-query'
import { SearchFormValues } from '../Header/Header'
import { Tabs, TabsList, TabsTrigger } from '../ui/tabs'
import Charts from './Charts/Charts'
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

	if (data.posts.length === 0) {
		return (
			<p className='text-center text-lg mt-80'>
				No results found. Try to change the filters or query.
			</p>
		)
	}

	return (
		<div className='xl:max-w-[1200px] md:max-w[700px] lg:max-w-[1000px] h-full w-full mx-auto mt-4 mb-16'>
			<Tabs
				defaultValue='feed'
				className='flex justify-center flex-col w-full items-center space-y-8'
			>
				<TabsList>
					<TabsTrigger value='feed'>Feed</TabsTrigger>
					<TabsTrigger value='charts'>Analytics</TabsTrigger>
				</TabsList>

				<TabsContent value='feed'>
					<Feed posts={data.posts} />
				</TabsContent>
				<TabsContent value='charts' className='w-full'>
					<Charts {...data} />
				</TabsContent>
			</Tabs>
		</div>
	)
}

export default Main
