import Link from "next/link";

interface TableHeaderProps {
    title: string;
}
const TableHeader = ({title}: TableHeaderProps)  => {
    return (
        <th scope="col" className="px-6 py-3">
            {title}
        </th>
    )
}

export default TableHeader;