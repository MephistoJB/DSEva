import Link from "next/link";
import { RepositoryType } from "./TableList";

interface TableRowProps {
    repository: RepositoryType;
}

const TableRow: React.FC<TableRowProps> = ({ 
    repository 
}) => {
    return (

        <tr className="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
            <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                {repository.title}
            </th>
{/*             <td className="px-6 py-4">
                Silver
            </td>
            <td className="px-6 py-4">
                Laptop
            </td>
            <td className="px-6 py-4">
                $2999
            </td>
            <td className="px-6 py-4">
                <a href="#" className="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit</a>
            </td> */}
        </tr>
    )
}

export default TableRow;