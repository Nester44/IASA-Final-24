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
	const data = mapPostsToData(posts)

	console.log(data)

	return (
		<div className='w-[600px] h-[400px]'>
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
					<Tooltip labelStyle={{ color: 'red' }} />
					<Legend />
					<Bar dataKey='twitter' stackId='a' fill='#8884d8' />
					<Bar dataKey='mctoday' stackId='a' fill='#82ca9d' />
					{/* |  | "bbc" | "cnn" | "breitbart" */}
				</BarChart>
			</ResponsiveContainer>
		</div>
	)
}

export default PostsTrend
