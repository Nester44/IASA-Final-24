import { SourceId, sourceIds } from '@/components/Header/Header'
import { Post } from '@/lib/api/fetchAnalytics'
import {
	Bar,
	BarChart,
	CartesianGrid,
	Legend,
	ResponsiveContainer,
	Tooltip,
	XAxis,
	YAxis,
} from 'recharts'
type Props = {
	posts: Post[]
}

type Data = {
	date: string
} & Record<SourceId, number>

const mapPostsToData = (posts: Post[]): Data[] => {
	const data: Record<string, any> = {}
	for (const post of posts) {
		const date = new Date(post.created * 1000).toDateString()
		if (!data[date]) {
			data[date] = {}
		}
		data[date][post.source.id] = (data[date][post.source.id] || 0) + 1
	}
	const result = []

	for (const key in data) {
		result.push({
			date: key,
			...data[key],
		})
	}

	for (const sourceId of sourceIds) {
		for (const item of result) {
			if (!item[sourceId]) {
				item[sourceId] = 0
			}
		}
	}
	return result
}

const PostsTrend = ({ posts }: Props) => {
	const data = mapPostsToData(posts).sort((a, b) => {
		const aDate = new Date(a.date)
		const bDate = new Date(b.date)
		return aDate.getTime() - bDate.getTime()
	})

	console.log(data)

	return (
		<div className='flex-grow-[2] h-[350px]'>
			<p className='text-center text-xl font-bold mb-8'>
				Posts trend over time by sources
			</p>
			<ResponsiveContainer width='100%' height='100%'>
				<BarChart
					width={500}
					height={300}
					data={data}
					margin={{
						top: 20,
						right: 30,
						left: 20,
						bottom: 5,
					}}
				>
					<CartesianGrid strokeDasharray='3 3' />
					<XAxis dataKey='date' />
					<YAxis min={0} max={32} />
					<Tooltip
						wrapperClassName='p-2 rounded-lg border shadow-lg'
						contentStyle={{ background: 'black', border: 'none' }}
					/>
					<Legend />
					{/* <Bar dataKey='twitter' stackId='a' fill='#1BA0F1' /> */}
					<Bar dataKey='mctoday' stackId='a' fill='#FFE043' />
					<Bar dataKey='cnn' stackId='a' fill='#FE0000' />
					<Bar dataKey='bbc-news' stackId='a' fill='#B80000' />
					<Bar dataKey='breitbart-news' stackId='a' fill='#FF5501' />
				</BarChart>
			</ResponsiveContainer>
		</div>
	)
}

export default PostsTrend
