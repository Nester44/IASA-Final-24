import { SearchFormValues, SourceId } from '@/components/Header/Header'
import { QueryFunctionContext } from '@tanstack/react-query'
import axios from 'axios'

const instance = axios.create({
	baseURL: import.meta.env.VITE_BACKEND_URL as string,
})

export type Source = {
	id: SourceId
	name: string
}

export type Post = {
	sentiment_rate: number
	content: string
	created: number
	source: Source
	id: number
}

export type Analytics = {
	total_positives: number
	total_negatives: number
	total_neutral: number
	posts: Post[]
	keywords: [
		{
			word: string
			occurences: number
		},
	]
}

export async function fetchAnalytics(
	context: QueryFunctionContext<[string, SearchFormValues]>,
) {
	const [_, { period, query, sources }] = context.queryKey

	const params = new URLSearchParams({
		period,
		q: query,
		sources: sources.join(','),
	})

	const response = await instance.get<Analytics>(`/analytics?${params}`)

	return response.data
}
