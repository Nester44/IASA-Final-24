import { Analytics } from '@/lib/api/fetchAnalytics'
import WordCloud from 'react-d3-cloud'

type Props = {} & Pick<Analytics, 'keywords'>

const Cloud = ({ keywords }: Props) => {
	const data = keywords.map(([text, value]) => ({ text, value: 1 / value }))

	return <WordCloud data={data} />
}

export default Cloud
