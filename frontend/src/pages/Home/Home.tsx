import Header, { SearchFormValues } from '@/components/Header/Header'
import Main from '@/components/Main/Main'
import MainLoader from '@/components/Main/MainLoader'
import { Suspense, useState } from 'react'

export const Home = () => {
	const [searchValues, setSearchValues] = useState<SearchFormValues>()

	return (
		<div>
			<Header onSubmit={setSearchValues} />

			<Suspense fallback={<MainLoader />}>
				<Main searchValues={searchValues} />
			</Suspense>
		</div>
	)
}
