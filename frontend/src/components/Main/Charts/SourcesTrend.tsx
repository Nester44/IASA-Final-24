import { SourceId } from '@/components/Header/Header'
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

const mapPostsToData = (posts: Post[]) => {
	const result = []

	const sentimentsBySource: Partial<
		Record<
			SourceId,
			{ negatives: number; neutrals: number; positives: number }
		>
	> = {}

	for (const post of posts) {
		const sourceId = post.source.id

		if (!sentimentsBySource[sourceId]) {
			sentimentsBySource[sourceId] = {
				negatives: 0,
				neutrals: 0,
				positives: 0,
			}
		}
	}

	for (const key in sentimentsBySource) {
		const sourceId = key as SourceId
		const a = sentimentsBySource[sourceId]

		if (!a) {
			continue
		}
		const { negatives, neutrals, positives } = a

		result.push({
			sourceId,
			negatives,
			neutrals,
			positives,
		})
	}

	return result
}

const SourcesTrend = ({ posts }: Props) => {
	const data = mapPostsToData(posts)
	console.log(data)
	return (
		<div className='w-[600px] h-[400px]'>
			{/* <ResponsiveContainer width='100%' height='100%'>
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
				</BarChart>
			</ResponsiveContainer> */}
		</div>
	)
}

export default SourcesTrend
